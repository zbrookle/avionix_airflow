# AWS EKS Setup Instructions

## Installation Requirements

1. VPC
2. At least 2 subnets in that VPC (These should be marked properly for load balancing
, see [alb-ingress](https://docs.aws.amazon.com/eks/latest/userguide/alb-ingress.html))
3. EKS Cluster
4. An aws EFS Volume

The above requirements can be created using [eksctl](https://eksctl.io/)

Avionix_airflow is also preconfigured to use [kube2iam](https://github.com/jtblin/kube2iam), 
which can be used to assign roles to your kubernetes pods

## Additional Requirements (Reccommended)

1. AWS ElasticSearch Cluster
    1. An IAM role that is authorized to connect to the cluster
2. Ensure that the security group for the cluster is allowed TCP access on port 443
 from the EKS cluster security group
 
After all of the above requirements are met, follow the main documentation.


 
 