# AWS EKS Setup Instructions

## Installation Requirements

1. VPC
2. At least 2 subnets in that VPC (These should be marked properly for load balancing
, see [alb-ingress](https://docs.aws.amazon.com/eks/latest/userguide/alb-ingress.html))
3. EKS Cluster

The above requirements can be created using [eksctl](https://eksctl.io/)

Avionix_airflow is also preconfigured to use [kube2iam](https://github.com/jtblin/kube2iam), 
which can be used to assign roles to your kubernetes pods

4. An aws EFS Volume (Be sure this is available in the same subnets as the cluster
 and the security group allows traffic from the cluster's security group)
5. An IAM role that is autorized to manipulate ALB's based on the subnet tags you
 wrote above. You can find a minimal policy for this [here](https://github.com/kubernetes-sigs/aws-alb-ingress-controller/blob/0338ed144f584c7a7738b4bf1d8ca8c827e7abb0/docs/examples/iam-policy.json#L117-L126)
6. An IAM role that can set up an record dns in route53. You can find information
 about the required policy [here](https://github.com/kubernetes-sigs/external-dns/blob/master/docs/tutorials/aws.md#iam-permissions)
## Additional Requirements (Reccommended)

1. AWS ElasticSearch Cluster
    1. An IAM role that is authorized to connect to the cluster
2. Ensure that the security group for the cluster is allowed TCP access on port 443
 from the EKS cluster security group

 
After all of the above requirements are met, follow the main documentation.


 
 