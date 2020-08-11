function process(event) {
    var dag_id = event.Get("kubernetes.labels.dag_id");
    var task_id = event.Get("kubernetes.labels.task_id");
    var try_number = event.Get("kubernetes.labels.try_number");
    var execution_date = event.Get("kubernetes.labels.execution_date");
    if (dag_id != null) {
      event.Put("log_id", dag_id + "-" + task_id + "-" + execution_date + "-" + try_number);
      var offset = event.Get("log.offset");
      event.Put("offset", offset);
    }
}
