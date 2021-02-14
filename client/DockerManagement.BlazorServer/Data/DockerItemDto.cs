using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace DockerManagement.BlazorServer.Data
{
    public class ContainerItemDto
    {
        public string short_id { get; set; }
        public string name { get; set; }
        public string image { get; set; }
        public string[] ports { get; set; }
        public string command { get; set; }
        public DateTime created { get; set; }
        public string status { get; set; }
        public DateTime started { get; set; }
        public DateTime ended { get; set; }
        public int exitcode { get; set; }
    }


    public class ImageItemDto
    {
        public string id { get; set; }
        public string short_id { get; set; }
        public string[] tags { get; set; }
    }
}
