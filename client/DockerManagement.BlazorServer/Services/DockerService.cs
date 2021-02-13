using DockerManagement.BlazorServer.Data;
using Microsoft.Extensions.Configuration;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;

namespace DockerManagement.BlazorServer.Services
{
    public class DockerService
    {
        private readonly HttpClient client;
        private readonly string baseUrl;

        public DockerService(IConfiguration configuration)
        {
            client = new HttpClient();
            baseUrl = configuration["BaseServerUrl"];
        }

        public async Task<ContainerItemDto[]> GetContainers()
        {
            return await client.GetFromJsonAsync<ContainerItemDto[]>($"{baseUrl}docker/containers");
        }

        public async Task<string> StopContainer(string idOrName)
        {
            return await client.GetStringAsync($"{baseUrl}docker/containers/stop/{idOrName}");
        }

        public async Task<ImageItemDto[]> GetImages()
        {
            return await client.GetFromJsonAsync<ImageItemDto[]>($"{baseUrl}docker/images");
        }

        public async Task<string> RemoveImageById(string idOrName)
        {
            return await client.GetStringAsync($"{baseUrl}docker/images/remove/{idOrName}");
        }
    }
}
