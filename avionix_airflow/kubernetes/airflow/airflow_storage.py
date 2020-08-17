from typing import List

from avionix.kube.core import (
    Container,
    LabelSelector,
    PersistentVolume,
    PersistentVolumeClaim,
    PersistentVolumeClaimSpec,
    PersistentVolumeClaimVolumeSource,
    PersistentVolumeSpec,
    ResourceRequirements,
    Volume,
    VolumeMount,
)

from avionix_airflow.kubernetes.airflow.airflow_options import AirflowOptions
from avionix_airflow.kubernetes.cloud.cloud_options import CloudOptions
from avionix_airflow.kubernetes.namespace_meta import AirflowMeta


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
    def __init__(self, name: str, volume_mount: VolumeMount):
        super().__init__(
            f"{name}-set-owner",
            image="busybox",
            command=["/bin/chmod", "777", volume_mount.mountPath],
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
            f"{name}-permission-container", self.__volume_mount
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
