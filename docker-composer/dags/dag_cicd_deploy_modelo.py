from airflow.sdk import DAG, task, TaskGroup
import requests
import pendulum



@task
def fazer_requisicao_post(path: str, verb: str = "POST"):
    url = f"http://api-datathon:8000/{path}"
    payload = ""
    headers = {}

    response = requests.request(verb, url, headers=headers, data=payload)
    print(response.text)


with DAG(
    dag_id="dag_cicd_deploy_modelo",
    catchup=False,
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    schedule=None,
    tags=["local", "deploy","api"],
) as dag:

    with TaskGroup(group_id="ingestao") as ingestao_group:
        dados_raw = fazer_requisicao_post.override(task_id="ingestao_raw")(
            path="ingestao/raw",
            verb="POST"
        )

        dados_trusted = fazer_requisicao_post.override(task_id="ingestao_trusted")(
            path="ingestao/trusted",
            verb="POST"
        )    
        
        dados_refined = fazer_requisicao_post.override(task_id="ingestao_refined")(
            path="ingestao/refined",
            verb="POST"
        )

        dados_raw >> dados_trusted >> dados_refined

    with TaskGroup(group_id="modelo") as deploy_group:
        deploy_modelo = fazer_requisicao_post.override(task_id="deploy_model")(
            path="model/deploy",
            verb="POST"
        )

        deploy_avaliacao = fazer_requisicao_post.override(task_id="deploy_avaliacao")(
            path="model/avaliacao",
            verb="POST"
        )
        deploy_modelo >> deploy_avaliacao        

    ingestao_group >> deploy_group