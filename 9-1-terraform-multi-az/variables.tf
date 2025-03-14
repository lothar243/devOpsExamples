variable "access_key" {
  type = string
  sensitive = false
}

variable "secret_key" {
  type = string
  sensitive = true
}

variable "public_subnet_cidrs" {
 type        = list(string)
 description = "Public Subnet CIDR values"
 default     = ["10.0.0.0/24", "10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
}

variable "private_subnet_cidrs" {
 type        = list(string)
 description = "Private Subnet CIDR values"
 default     = ["10.0.128.0/24", "10.0.129.0/24", "10.0.130.0/24", "10.0.131.0/24"]
}

variable "region" {
  type = string
  sensitive = false
  default = "us-east-1"
}

variable "availability_zones" {
 type        = list(string)
 description = "Availability Zones"
 default     = ["us-east-1a", "us-east-1b"]
}

variable "ami" {
    type     = string
    description = "Amazon Machine Image to Use"
}