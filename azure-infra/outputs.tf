#public ip address of azure machine
output "azure_vm_public_ip" {
  value = azurerm_public_ip.public_ip.ip_address
}