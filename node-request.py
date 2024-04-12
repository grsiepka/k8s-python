# Python script to gather CPU request across nodes in a given nodepool. 
# Needs kubernetes python library. 
# https://github.com/kubernetes-client/python
# Replace "your-node-pool-name" with the actual name of your node pool.
# Replace "your-context-name" with the name of the context corresponding to the Kubernetes cluster you want to target

from kubernetes import client, config

def get_cpu_requests_per_node(node_pool_label_selector, kube_context):
    # Load kubeconfig file with the specified context
    config.load_kube_config(context=kube_context)

    # Create Kubernetes API client
    api_instance = client.CoreV1Api()

    try:
        # Define label selector to filter nodes by node pool
        label_selector = f"cloud.google.com/gke-nodepool={node_pool_label_selector}"

        # Retrieve list of nodes with the specified label selector
        nodes = api_instance.list_node(label_selector=label_selector).items

        cpu_requests_per_node = {}

        # Iterate over each node
        for node in nodes:
            node_name = node.metadata.name
            cpu_requests_per_node[node_name] = 0

            # Retrieve node's allocatable resources
            allocatable_resources = node.status.allocatable

            # Get CPU requests
            cpu_requests = allocatable_resources.get("cpu")

            if cpu_requests:
                cpu_requests_per_node[node_name] = cpu_requests

        return cpu_requests_per_node

    except Exception as e:
        print("Exception when calling CoreV1Api->list_node: %s\n" % e)

if __name__ == "__main__":
    # Specify the node pool label selector
    node_pool_label_selector = "your-node-pool-name"

    # Specify the Kubernetes context
    kube_context = "your-context-name"

    cpu_requests_per_node = get_cpu_requests_per_node(node_pool_label_selector, kube_context)
    print("CPU requests per Kubernetes node in node pool", node_pool_label_selector)
    for node, cpu_requests in cpu_requests_per_node.items():
        print(f"{node}: {cpu_requests}")
