let data = [
  {
    "Host": "aki-ems-pp01",
    "Ip": "10.173.25.96",
    "Host group": "Hors-Prod",
    "Operating System": "RedHat 7.7",
    "Critical": 0,
    "Important": 38,
    "Moderate": 44,
    "Low": 15
  },
  {
    "Host": "example-host-02",
    "Ip": "192.168.1.100",
    "Host group": "Prod",
    "Operating System": "Ubuntu 20.04",
    "Critical": 2,
    "Important": 25,
    "Moderate": 30,
    "Low": 8
  },
  {
    "Host": "test-server-01",
    "Ip": "10.10.10.10",
    "Host group": "Test",
    "Operating System": "CentOS 8",
    "Critical": 1,
    "Important": 20,
    "Moderate": 15,
    "Low": 5
  },
 {
    "Host": "example-host-03",
    "Ip": "192.168.1.101",
    "Host group": "Prod",
    "Operating System": "CentOS 7",
    "Critical": 3,
    "Important": 22,
    "Moderate": 28,
    "Low": 10
  },
  {
    "Host": "test-server-02",
    "Ip": "10.10.10.11",
    "Host group": "Test",
    "Operating System": "Ubuntu 18.04",
    "Critical": 2,
    "Important": 18,
    "Moderate": 20,
    "Low": 7
  },
  {
    "Host": "dev-machine-01",
    "Ip": "192.168.2.50",
    "Host group": "Dev",
    "Operating System": "Windows Server 2019",
    "Critical": 1,
    "Important": 12,
    "Moderate": 15,
    "Low": 4
  },
  {
    "Host": "backup-server-01",
    "Ip": "10.20.30.40",
    "Host group": "Backup",
    "Operating System": "Ubuntu 16.04",
    "Critical": 0,
    "Important": 8,
    "Moderate": 10,
    "Low": 2
  },
  {
    "Host": "db-server-01",
    "Ip": "10.50.60.70",
    "Host group": "Database",
    "Operating System": "Oracle Linux 7",
    "Critical": 4,
    "Important": 35,
    "Moderate": 40,
    "Low": 12
  },
  {
    "Host": "web-server-01",
    "Ip": "10.100.200.300",
    "Host group": "Web",
    "Operating System": "Debian 10",
    "Critical": 2,
    "Important": 28,
    "Moderate": 30,
    "Low": 9
  },
  {
    "Host": "example-host-04",
    "Ip": "192.168.1.102",
    "Host group": "Prod",
    "Operating System": "RedHat 8",
    "Critical": 1,
    "Important": 20,
    "Moderate": 25,
    "Low": 6
  },
  {
    "Host": "test-server-03",
    "Ip": "10.10.10.12",
    "Host group": "Test",
    "Operating System": "CentOS 7",
    "Critical": 2,
    "Important": 15,
    "Moderate": 18,
    "Low": 5
  },
  {
    "Host": "example-host-05",
    "Ip": "192.168.1.103",
    "Host group": "Prod",
    "Operating System": "Ubuntu 20.04",
    "Critical": 0,
    "Important": 28,
    "Moderate": 32,
    "Low": 10
  },
  {
    "Host": "monitoring-server-01",
    "Ip": "10.20.30.50",
    "Host group": "Monitoring",
    "Operating System": "Ubuntu 18.04",
    "Critical": 1,
    "Important": 10,
    "Moderate": 12,
    "Low": 3
  },
{
    "Host": "example-host-06",
    "Ip": "192.168.1.104",
    "Host group": "Prod",
    "Operating System": "CentOS 8",
    "Critical": 0,
    "Important": 30,
    "Moderate": 35,
    "Low": 8
  },
  {
    "Host": "test-server-04",
    "Ip": "10.10.10.13",
    "Host group": "Test",
    "Operating System": "Ubuntu 20.04",
    "Critical": 1,
    "Important": 20,
    "Moderate": 22,
    "Low": 6
  },
  {
    "Host": "example-host-07",
    "Ip": "192.168.1.105",
    "Host group": "Prod",
    "Operating System": "RedHat 7.6",
    "Critical": 2,
    "Important": 18,
    "Moderate": 20,
    "Low": 7
  },
  {
    "Host": "test-server-05",
    "Ip": "10.10.10.14",
    "Host group": "Test",
    "Operating System": "CentOS 8",
    "Critical": 1,
    "Important": 25,
    "Moderate": 28,
    "Low": 9
  },
  {
    "Host": "example-host-08",
    "Ip": "192.168.1.106",
    "Host group": "Prod",
    "Operating System": "Ubuntu 18.04",
    "Critical": 0,
    "Important": 22,
    "Moderate": 25,
    "Low": 6
  },
  {
    "Host": "dev-machine-02",
    "Ip": "192.168.2.51",
    "Host group": "Dev",
    "Operating System": "Windows 10",
    "Critical": 1,
    "Important": 15,
    "Moderate": 18,
    "Low": 5
  },
  {
    "Host": "example-host-09",
    "Ip": "192.168.1.107",
    "Host group": "Prod",
    "Operating System": "CentOS 7",
    "Critical": 1,
    "Important": 20,
    "Moderate": 22,
    "Low": 5
  },
  {
    "Host": "test-server-06",
    "Ip": "10.10.10.15",
    "Host group": "Test",
    "Operating System": "Ubuntu 16.04",
    "Critical": 0,
    "Important": 12,
    "Moderate": 15,
    "Low": 3
  },
  {
    "Host": "example-host-10",
    "Ip": "192.168.1.108",
    "Host group": "Prod",
    "Operating System": "RedHat 8",
    "Critical": 2,
    "Important": 25,
    "Moderate": 28,
    "Low": 8
  },
  {
    "Host": "backup-server-02",
    "Ip": "10.20.30.60",
    "Host group": "Backup",
    "Operating System": "Ubuntu 20.04",
    "Critical": 0,
    "Important": 10,
    "Moderate": 12,
    "Low": 2
  },
{
    "Host": "example-host-10",
    "Ip": "192.168.1.108",
    "Host group": "Prod",
    "Operating System": "Ubuntu 20.04",
    "Critical": 0,
    "Important": 28,
    "Moderate": 32,
    "Low": 9
  },
  {
    "Host": "test-server-07",
    "Ip": "10.10.10.16",
    "Host group": "Test",
    "Operating System": "CentOS 8",
    "Critical": 2,
    "Important": 20,
    "Moderate": 25,
    "Low": 8
  },
  {
    "Host": "example-host-11",
    "Ip": "192.168.1.109",
    "Host group": "Prod",
    "Operating System": "RedHat 7.8",
    "Critical": 2,
    "Important": 25,
    "Moderate": 30,
    "Low": 7
  },
  {
    "Host": "test-server-08",
    "Ip": "10.10.10.17",
    "Host group": "Test",
    "Operating System": "Ubuntu 20.04",
    "Critical": 1,
    "Important": 18,
    "Moderate": 22,
    "Low": 6
  },
  {
    "Host": "example-host-12",
    "Ip": "192.168.1.110",
    "Host group": "Prod",
    "Operating System": "CentOS 7",
    "Critical": 0,
    "Important": 22,
    "Moderate": 26,
    "Low": 5
  },
  {
    "Host": "backup-server-03",
    "Ip": "10.20.30.70",
    "Host group": "Backup",
    "Operating System": "Ubuntu 20.04",
    "Critical": 1,
    "Important": 10,
    "Moderate": 15,
    "Low": 4
  },
  {
    "Host": "db-server-03",
    "Ip": "10.50.60.90",
    "Host group": "Database",
    "Operating System": "Oracle Linux 8",
    "Critical": 2,
    "Important": 32,
    "Moderate": 38,
    "Low": 11
  },
  {
    "Host": "web-server-03",
    "Ip": "10.100.200.302",
    "Host group": "Web",
    "Operating System": "Debian 11",
    "Critical": 1,
    "Important": 25,
    "Moderate": 28,
    "Low": 8
  },
  {
    "Host": "example-host-13",
    "Ip": "192.168.1.111",
    "Host group": "Prod",
    "Operating System": "RedHat 8",
    "Critical": 1,
    "Important": 18,
    "Moderate": 22,
    "Low": 6
  },
  {
    "Host": "test-server-09",
    "Ip": "10.10.10.18",
    "Host group": "Test",
    "Operating System": "CentOS 7",
    "Critical": 0,
    "Important": 15,
    "Moderate": 20,
    "Low": 4
  }

]

let para =document.getElementById("#para")

para.addEventListener('click', ee =>{
  console.log("clic")
})