import argparse
import os

from langchain.agents import tool
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from src.prod.crossplane.agent_crossplane_oneshot import (
    CrossplaneDeploymentGenerator, _sanitize_output_loop, apply_yaml,
    search_db)
from src.prod.github.agent_github_oneshot import GithubSearchAgent
from src.prod.github.github_connector import GithubConnector
from src.prod.kubernetes.agent_kubernetes import (
    KubernetesDeploymentGenerator, _sanitize_output_loop)

# Initialize the command-line argument parsing
parser = argparse.ArgumentParser(
    description="Run Pipeline for the base model, but with an agent instead of a chain for the Kubernetes Generator."
)
parser.add_argument(
    "--name",
    type=str,
    help="Name of the file or folder to navigate.",
    default="Crossplane-Automation-Tests/llm-vector-test-no-docker",
)
parser.add_argument(
    "--question",
    type=str,
    help="Question to ask about the repository.",
    default="How could a potential Dockerfile for this repository look like?",
)
parser.add_argument(
    "--input",
    type=str,
    help="Name of the file or folder to navigate.",
    default="I want to deploy my database on aws with BTP authentication.",
)

args = parser.parse_args()


@tool
def navigate_github(command: str) -> str:
    """Fetches the content of a specified GitHub file or the contents of a specified folder.
    Users can navigate through the GitHub repository by specifying the name of a file or folder.
    Use 'BACK' to go back if needed.
    Use 'HERE' to display the current files.
    """
    output = github.navigate_github_files(command)
    return str(output)


@tool
def generate_crossplane(component_name: str) -> str:
    """This method takes a 'component_name' searches the OpensSearch Index for its definition, generates a suitable component and saves it to a file. Returns the status of the operation."""

    db_doc = search_db(component_name, index_name, client, 1)["hits"]["hits"][0][
        "_source"
    ]["content"]

    template_loop = (
        "Write yaml code to create a template based on the schema of the specified crossplane component. Take necessary information from the given documentation, but make the simplest definition possible."
        "Never use placeholders, only comment them!"
        "The code has to be runnable and functional. "
        "Return only yaml code in Markdown format, e.g.: ```yaml .... ```"
        """For example given the schema:
                - apiVersion: apiextensions.k8s.io/v1
  kind: CustomResourceDefinition
  metadata:
    annotations:
      controller-gen.kubebuilder.io/version: v0.13.0
    name: kymaenvironments.environment.btp.orchestrate.cloud.sap
  spec:
    group: environment.btp.orchestrate.cloud.sap
    names:
      categories: [crossplane, managed, btp]
      kind: KymaEnvironment
      listKind: KymaEnvironmentList
      plural: kymaenvironments
      singular: kymaenvironment
    scope: Cluster
    versions:
    - additionalPrinterColumns: [...]
      name: v1alpha1
      schema:
        openAPIV3Schema:
          description: A KymaEnvironment is an example API type.
          properties:
            apiVersion: {description: 'APIVersion defines the versioned schema...', type: string}
            kind: {description: 'Kind is a string value representing...', type: string}
            metadata: {type: object}
            spec:
              description: A KymaEnvironmentSpec defines the desired state of a KymaEnvironment.
              properties:
                cloudManagementRef:
                  description: A Reference to a named object.
                  properties: {name: {description: Name of the referenced object., type: string}, policy: {...}}
                  required: [name]
                  type: object
                cloudManagementSecret: {type: string}
                cloudManagementSecretNamespace: {type: string}
                cloudManagementSelector: {...}
                cloudManagementSubaccountGuid: {type: string}
                deletionPolicy: {default: Delete, description: 'DeletionPolicy specifies...', enum: [Orphan, Delete], type: string}
                forProvider:
                  description: KymaEnvironmentParameters are the configurable fields of a KymaEnvironment.
                  properties:
                    parameters: {...}
                    planName: {type: string}
                  required: [planName]
                  type: object
                ...
              required: [forProvider]
              type: object
            status:
              description: A KymaEnvironmentStatus represents the observed state...
              properties:
                atProvider: {...}
                conditions: [...]
              type: object
          required: [spec]
          type: object
      served: true
      storage: true
      subresources: {status: {}}


        !!This would be the template you should return in this case, e.g.!!:
        ```yaml
apiVersion: oidc.orchestrate.cloud.sap/v1alpha1
kind: CertBasedOIDCLogin
metadata:
  name: my-kyma-login
spec:
  writeConnectionSecretToRef:
    name: kyma-oidc-token
    namespace: default
  forProvider:
    clientId: <IDP Client ID>
    issuer: <IDP url>
    certificate:
      source: Secret
      secretRef:
        key: cert
        name: example-login-cert-secret
        namespace: default
    password:
      source: Secret
      secretRef:
        key: password
        name: keystore-secret
        namespace: default```
        """
    )

    prompt_template = ChatPromptTemplate.from_messages(
        [("system", template_loop), ("human", "{input}")]
    )
    chain_component = prompt_template | llm | StrOutputParser() | _sanitize_output_loop
    return apply_yaml(
        chain_component.invoke({"input": db_doc}), component_name, kube_path
    )


@tool
def get_services(query: str) -> str:
    """
    This function takes a 'query' and returns the response from the OpenSearch index.
    The index contains the latest definitions and names of crossplane resources.
    It does act as a single source of truth for the names of the resources.
    It does not return any thoughts about the system setup.
    The response contains always the confidence score and the name of the service, related to the given query.
    Only return one out of the five results, which matches the reuqirements the best.
    """

    parsed_return = []
    for i in search_db(query, index_name, client)["hits"]["hits"]:
        parsed_return.append((i["_score"], i["_source"]["service_name"]))

    return str(parsed_return)


@tool
def get_files_overview(inp: str) -> str:
    """
    This function lists all file names in the kube_path folder
    and returns them in a comma-separated string.
    """
    files = os.listdir(kube_path)
    return ", ".join(files)


@tool
def get_file_content(file_name: str) -> str:
    """
    This function takes a 'file_name' and returns the content of the file.
    The file name is expected to be a valid file within the kube_path directory.
    """
    with open(os.path.join(kube_path, file_name), "r") as file:
        content = file.read()
    return content


@tool
def verify_completion() -> str:
    """
    This function checks the status of the cluster and returns a message indicating overall health
    or the names of any resources that are not healthy.
    """
    return deployment_generator.connector.get_cluster_status(detail=True)


@tool
def generate_kubernetes(description: str) -> str:
    """This method takes in a description of a Kubernetes component and generates the necessary yaml code to create it.
    It returns the status of the code."""

    template_loop = (
        "You are a very powerful cloud architect, who transforms, a Dockerfile and a name into one kubernetes component. Think outside the box and make it as compatible as possible."
        "Write yaml code to create the specified component. Include all the necessary information and be precise, "
        "never use placeholders, only comment them! However, the code has to be runnable and functional. "
        "If there is an error being parsed in, try to fix it. Return only yaml code in Markdown format, e.g.: ```yaml .... ```"
        """For example when tasked to create a deployment for the application of a given Dockerfile, you should come up with something like this:
            ```yaml
            apiVersion: v1
                kind: Secret
                metadata:
                name: llm-configuration
                annotations:
                    avp.kubernetes.io/path: "onboarding/data/dev/llm-test"
                type: Opaque
                stringData:
                CLIENT_ID: <client-id>
                CLIENT_SECRET: <client-secret>
                DATABASE_URL: <database-url>
                ---
                apiVersion: apps/v1
                kind: Deployment
                metadata:
                name: llm-test
                spec:
                selector:
                    matchLabels:
                    app: llm-test
                template:
                    metadata:
                    labels:
                        app: llm-test
                    spec:
                    imagePullSecrets:
                        - name: deploy-releases-hyperspace-docker
                    containers:
                    - name: llm-test
                        image: deploy-releases
                        envFrom:
                        - secretRef:
                            name: llm-configuration
                        ports:
                        - containerPort: 3001
                ---
                apiVersion: v1
                kind: Service
                metadata:
                name: llm-test
                spec:
                selector:
                    app: llm-test
                ports:
                - port: 3001
                    targetPort: 3001
                ```"""
    )

    prompt_template = ChatPromptTemplate.from_messages(
        [("system", template_loop), ("human", "{input}")]
    )
    chain_component = (
        prompt_template
        | deployment_generator.llm
        | StrOutputParser()
        | _sanitize_output_loop
    )
    out_text = deployment_generator.connector.apply_yaml(
        chain_component.invoke(
            {"input": description + deployment_generator.dockerfile_content}
        )
    )

    return out_text


if __name__ == "__main__":

    # Github seracher agent
    github = GithubConnector(
        name=args.name, token=os.getenv("OAUTH_TOKEN_GH_ENTERPRISE_TOOLS")
    )
    search_agent = GithubSearchAgent(github, [navigate_github], power=True)
    result = search_agent.execute_search(args.question)[-1]

    input("Press Enter to continue...")

    deployment_generator = KubernetesDeploymentGenerator(
        dockerfile_content=str(result["output"]),
        tools=[generate_kubernetes, verify_completion],
        power=True,
    )
    deployment_generator.execute_search()

    input("Press Enter to continue...")

    # Crossplane generation agent
    generator = CrossplaneDeploymentGenerator(
        args.input,
        tools=[generate_crossplane, get_services, get_files_overview, get_file_content],
        power=True,
        kube_path=deployment_generator.connector.dir,
    )
    kube_path = generator._kube_path
    llm = generator._llm
    index_name = generator._index_name
    client = generator._client
    response = generator.execute_search()
