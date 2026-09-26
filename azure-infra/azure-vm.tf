#linux virtual machine

resource "azurerm_linux_virtual_machine" "my_vm" {
  name                = "RoadGuardAI"
  location            = azurerm_resource_group.my_rg.location
  resource_group_name = azurerm_resource_group.my_rg.name

  admin_username = "azureuser"

  network_interface_ids = [
    azurerm_network_interface.nic.id
  ]

  # 4 vCPU / 16 GB RAM
  size = "Standard_B4ms"


  # SSH KEY
  admin_ssh_key {
    username   = "azureuser"
    public_key = file(pathexpand("~/.ssh/id_ed25519.pub"))
  }


  # OS DISK
  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Premium_LRS"
    disk_size_gb         = 64
  }


  # Ubuntu 24.04 LTS
  source_image_reference {
    publisher = "Canonical"
    offer     = "ubuntu-24_04-lts"
    sku       = "server"
    version   = "latest"
  }
}