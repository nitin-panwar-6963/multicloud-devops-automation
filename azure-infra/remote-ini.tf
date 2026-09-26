resource "local_file" "inventory_file" {
  filename = "${path.module}/ansible/host.ini"

  content = <<-EOT
[servers]
worker-node-1 ansible_host=${azurerm_linux_virtual_machine.my_vm.public_ip_address} ansible_user=azureuser

[all:vars]
ansible_ssh_private_key_file=/home/nitin/.ssh/id_ed25519
ansible_python_interpreter=/usr/bin/python3
EOT
}