provider "aws" {
 region = "ap-south-1"
}

resource "aws_instance" "ec2" {

 ami = "ami-02d26659fd82cf299"
 instance_type = "t2.micro"
 key_name = "Dev"
 vpc_security_group_ids = ["sg-0e065bb549317996c"]
 
 user_data = file("script.sh")

 tags = {
 Name = "Terra"
 volumes = "Terra" 
 } 

}

# ✅ Outputs
output "ec2_public_ip" {
  description = "Public IP of the EC2 instance"
  value       = aws_instance.ec2.public_ip
}
