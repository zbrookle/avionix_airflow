from abc import ABC, abstractmethod
from typing import List, Optional

from avionix.kube.core import (
    ConfigMapVolumeSource,
    Container,
    KeyToPath,
    LabelSelector,
    PersistentVolume,
    PersistentVolumeClaim,
    PersistentVolumeClaimSpec,
    PersistentVolumeClaimVolumeSource,
    PersistentVolumeSpec,
    ResourceRequirements,
    SecretVolumeSource,
    Volume,
    VolumeMount,
)

from avionix_airflow.kubernetes.airflow.airflow_options import AirflowOptions
from avionix_airflow.kubernetes.cloud.cloud_options import CloudOptions
from avionix_airflow.kubernetes.namespace_meta import AirflowMeta
from avionix_airflow.kubernetes.value_handler import ValueOrchestrator


class AirflowPersistentVolume(PersistentVolume):
    def __init__(
        self,
        name: str,
        storage: str,
        host_path: str,
        access_modes: List[str],
        cloud_options: CloudOptions,
    ):
        self._cloud_options = cloud_options
        volume_spec = PersistentVolumeSpec(
            access_modes,
            capacity={"storage": storage},
            host_path=self._cloud_options.get_host_path_volume_source(host_path),
            storage_class_name=self._cloud_options.storage_class.metadata.name,
            volume_mode=self._cloud_options.volume_mode,
            csi=self._cloud_options.get_csi_persistent_volume_source(name),
        )

        super().__init__(
            AirflowMeta(
                name,
                annotations={"pv.beta.kubernetes.io/gid": "1001"},
                labels={"storage-type": name},
            ),
            volume_spec,
        )


class AirflowVolume(Volume):
    def __init__(self, name: str, claim_name: str):
        super().__init__(
            name,
            persistent_volume_claim=PersistentVolumeClaimVolumeSource(
                claim_name, read_only=False
            ),
        )


class AirflowPersistentVolumeClaim(PersistentVolumeClaim):
    def __init__(
        self,
        name: str,
        access_modes: List[str],
        storage: str,
        cloud_options: CloudOptions,
    ):
        self._cloud_options = cloud_options
        super().__init__(
            AirflowMeta(name),
            PersistentVolumeClaimSpec(
                access_modes,
                resources=ResourceRequirements(requests={"storage": storage}),
                selector=LabelSelector({"storage-type": name}),
                storage_class_name=self._cloud_options.storage_class.metadata.name,
            ),
        )


class AirflowVolumeMount(VolumeMount):
    def __init__(self, name: str, folder: str):
        super().__init__(
            name, mount_path="/usr/local/airflow/" + folder, mount_propagation=None
        )


class PermissionSettingContainer(Container):
    def __init__(
        self,
        name: str,
        volume_mount: VolumeMount,
        permission_bits: int = 777,
        path_to_file: Optional[str] = None,
    ):
        permission_path = volume_mount.mountPath if not path_to_file else path_to_file
        super().__init__(
            f"{name}-permission-container-set-owner",
            image="busybox",
            command=["/bin/chmod", str(permission_bits), permission_path],
            volume_mounts=[volume_mount],
        )


class AirflowPersistentVolumeGroup:
    def __init__(
        self,
        name: str,
        storage: str,
        access_modes: List[str],
        folder: str,
        cloud_options: CloudOptions,
    ):
        host_path = "/tmp/data/airflow/" + folder
        self.__volume = AirflowVolume(name, name)
        self.__persistent_volume = AirflowPersistentVolume(
            name, storage, host_path, access_modes, cloud_options
        )
        self.__persistent_volume_claim = AirflowPersistentVolumeClaim(
            self.__volume.persistentVolumeClaim.claimName,
            access_modes,
            storage,
            cloud_options,
        )
        self.__volume_mount = AirflowVolumeMount(name, folder=folder)
        self.__permission_container = PermissionSettingContainer(
            name, self.__volume_mount
        )

    @property
    def persistent_volume(self):
        return self.__persistent_volume

    @property
    def volume(self):
        return self.__volume

    @property
    def persistent_volume_claim(self):
        return self.__persistent_volume_claim

    @property
    def volume_mount(self):
        return self.__volume_mount

    @property
    def permission_container(self):
        return self.__permission_container


class AirflowLogVolumeGroup(AirflowPersistentVolumeGroup):
    def __init__(self, airflow_options: AirflowOptions, cloud_options: CloudOptions):
        super().__init__(
            "logs",
            airflow_options.log_storage,
            access_modes=airflow_options.access_modes,
            folder="logs",
            cloud_options=cloud_options,
        )


class AirflowDagVolumeGroup(AirflowPersistentVolumeGroup):
    def __init__(self, airflow_options: AirflowOptions, cloud_options: CloudOptions):
        super().__init__(
            "dags",
            airflow_options.dag_storage,
            access_modes=airflow_options.access_modes,
            folder="dags",
            cloud_options=cloud_options,
        )


class ExternalStorageVolumeGroup(AirflowPersistentVolumeGroup):
    def __init__(self, airflow_options: AirflowOptions, cloud_options: CloudOptions):
        super().__init__(
            "tmp",
            airflow_options.dag_storage,
            access_modes=airflow_options.access_modes,
            folder="tmp",
            cloud_options=cloud_options,
        )


class AirflowVolumeGroup(ABC):
    volume_name = "a_name"
    folder_path = "/path/to/folder"
    read_only: Optional[bool] = None
    sub_path: Optional[str] = None

    @property
    @abstractmethod
    def volume(self) -> Volume:
        pass

    @property
    def volume_mount(self) -> VolumeMount:
        return VolumeMount(
            self.volume_name,
            self.folder_path,
            read_only=self.read_only,
            sub_path=self.sub_path,
        )


class AirflowSSHSecretsVolumeGroup(AirflowVolumeGroup):
    volume_name = "ssh-key-volume"
    folder_path = "/root/.ssh/id_rsa"
    read_only = False
    sub_path = "id_rsa"

    @property
    def volume(self):
        return Volume(
            self.volume_name,
            secret=SecretVolumeSource(
                False,
                ValueOrchestrator().secret_name,
                items=[KeyToPath("gitSshKey", "id_rsa", 256)],
            ),
        )


class AirflowWorkerPodTemplateStorageGroup(AirflowVolumeGroup):
    volume_name = "worker-pod-template"
    folder_path = "/usr/local/airflow/worker_pod_template"

    @property
    def volume(self):
        return Volume(
            self.volume_name,
            config_map=ConfigMapVolumeSource(
                ValueOrchestrator().airflow_worker_pod_template_config_file,
                optional=False,
                items=[
                    KeyToPath(
                        ValueOrchestrator().airflow_worker_pod_template_config_file,
                        "pod_template.yaml",
                    )
                ],
            ),
        )
