# RESOURCE GROUP

resource "azurerm_resource_group" "my_rg" {
  name     = "nitin-terra-india"
  location = "India South Central"

  tags = {
    Project     = "RoadGuardAI"
    Description = "Infrastructure for Ansible and Docker"
    Environment = var.env
  }
}

# VIRTUAL NETWORK
resource "azurerm_virtual_network" "my_vpc" {
  name                = var.vpc_nmae
  location            = azurerm_resource_group.my_rg.location
  resource_group_name = azurerm_resource_group.my_rg.name

  address_space = ["10.0.0.0/16"]
  tags = {
    Description = "vitual private cloud for the Roadguard_Ai"
    Environment = var.env
  }
}



# SUBNET
resource "azurerm_subnet" "my_subnet" {
  name                 = var.subnet_name
  resource_group_name  = azurerm_resource_group.my_rg.name
  virtual_network_name = azurerm_virtual_network.my_vpc.name

  address_prefixes = ["10.0.1.0/24"]
  tags = {
    Description = "Subnet for the Roadguard_Ai "
    Environment = var.env
  }
}

# PUBLIC IP
resource "azurerm_public_ip" "public_ip" {
  name                = "var.public_ip"
  resource_group_name = azurerm_resource_group.my_rg.name
  location            = azurerm_resource_group.my_rg.location

  allocation_method = "Static"
  sku               = "Standard"
  tags = {
    Description = "IP configuration for the virtual machine"
    Environment = var.env
  }
}