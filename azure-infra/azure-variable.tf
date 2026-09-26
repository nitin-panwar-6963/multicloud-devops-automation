# Create variables for the Azure machine

# Environment variable
variable "env" {
  type        = string
  description = "Used for the environment {dev, prod}"
}

# Variable for virtual machine name
variable "linux_machine" {
  type        = string
  description = "Virtual machine name"
}

# For the VPC name
variable "vpc_name" {
  type        = string
  description = "For the VPC name"
}

# For subnet configuration
variable "subnet_name" {
  type        = string
  description = "Subnet name"
}

# For public IP
variable "public_ip" {
  type        = string
  description = "Public IP name"
}

# For network interface
variable "network_interface" {
  type        = string
  description = "Network interface name"
}

# For security group
variable "security_group_name" {
  type        = string
  description = "Security group name"
}