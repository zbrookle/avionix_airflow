from avionix_airflow import SmtpNotificationOptions


def test_smtp_settings():
    notification_options = SmtpNotificationOptions(
        "my.host", True, False, "user", "****", 1234, "me@mail.com"
    )
    assert notification_options.to_dict() == {
        "AIRFLOW__SMTP__SMTP_HOST": "my.host",
        "AIRFLOW__SMTP__SMTP_STARTTLS": "True",
        "AIRFLOW__SMTP__SMTP_SSL": "False",
        "AIRFLOW__SMTP__SMTP_USER": "user",
        "AIRFLOW__SMTP__SMTP_PASSWORD": "****",
        "AIRFLOW__SMTP__SMTP_PORT": "1234",
        "AIRFLOW__SMTP__SMTP_MAIL_FROM": "me@mail.com",
        "AIRFLOW__KUBERNETES_ENVIRONMENT_VARIABLES__"
        "AIRFLOW__SMTP__SMTP_HOST": "my.host",
        "AIRFLOW__KUBERNETES_ENVIRONMENT_VARIABLES__"
        "AIRFLOW__SMTP__SMTP_STARTTLS": "True",
        "AIRFLOW__KUBERNETES_ENVIRONMENT_VARIABLES__"
        "AIRFLOW__SMTP__SMTP_SSL": "False",
        "AIRFLOW__KUBERNETES_ENVIRONMENT_VARIABLES__"
        "AIRFLOW__SMTP__SMTP_USER": "user",
        "AIRFLOW__KUBERNETES_ENVIRONMENT_VARIABLES__"
        "AIRFLOW__SMTP__SMTP_PASSWORD": "****",
        "AIRFLOW__KUBERNETES_ENVIRONMENT_VARIABLES__"
        "AIRFLOW__SMTP__SMTP_PORT": "1234",
        "AIRFLOW__KUBERNETES_ENVIRONMENT_VARIABLES__"
        "AIRFLOW__SMTP__SMTP_MAIL_FROM": "me@mail.com",
    }
