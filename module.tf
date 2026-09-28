module "azure" {
  source = "./azure-infra/"

  env                 = "dev"
  linux_machine       = "Roadguard_Ai"
  vpc_name            = "roadguard-vnet"
  subnet_name         = "roadguard-subnet"
  public_ip           = "roadguard-public-ip"
  network_interface   = "roadguard-nic"
  security_group_name = "roadguard-nsg"
}