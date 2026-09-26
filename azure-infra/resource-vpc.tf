# RESOURCE GROUP

resource "azurerm_resource_group" "my_rg" {
  name     = "nitin-terra-india"
  location = "India South Central"

  tags = {
    Project     = "RoadGuardAI"
    Description = "Infrastructure for Ansible and Docker"
  }
}

# VIRTUAL NETWORK
resource "azurerm_virtual_network" "my_vpc" {
  name                = "nitin-vpc"
  location            = azurerm_resource_group.my_rg.location
  resource_group_name = azurerm_resource_group.my_rg.name

  address_space = ["10.0.0.0/16"]
}



# SUBNET
resource "azurerm_subnet" "my_subnet" {
  name                 = "nitin-subnet"
  resource_group_name  = azurerm_resource_group.my_rg.name
  virtual_network_name = azurerm_virtual_network.my_vpc.name

  address_prefixes = ["10.0.1.0/24"]
}

# PUBLIC IP
resource "azurerm_public_ip" "public_ip" {
  name                = "nitin-public-ip"
  resource_group_name = azurerm_resource_group.my_rg.name
  location            = azurerm_resource_group.my_rg.location

  allocation_method = "Static"
  sku               = "Standard"
}