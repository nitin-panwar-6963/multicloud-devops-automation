tf
# generally use to create caddy file for the app

resource "local_file" "caddy_file"{
   filename =  "../ansible/azure/roles/docker/files/Caddyfile"
   content = <<-EOT
     # you've assigned a Static Public IP in Azure), update this one line to
# match the new IP and run: docker compose up -d --build caddy
${azurerm_linux_virtual_machine.my_vm.public_ip_address}.nip.io {
    reverse_proxy frontend:100
}

EOT


}
