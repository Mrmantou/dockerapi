# https://hub.docker.com/_/microsoft-dotnet
FROM mcr.microsoft.com/dotnet/sdk:5.0 AS build
WORKDIR /source

# copy csproj and restore as distinct layers
COPY *.sln .
COPY DockerManagement.BlazorServer/*.csproj ./DockerManagement.BlazorServer/
RUN dotnet restore DockerManagement.BlazorServer/DockerManagement.BlazorServer.csproj

# copy everything else and build app
COPY DockerManagement.BlazorServer/. ./DockerManagement.BlazorServer/
WORKDIR /source/DockerManagement.BlazorServer
RUN dotnet publish -c release -o /app --no-restore

# final stage/image
FROM mcr.microsoft.com/dotnet/aspnet:5.0
WORKDIR /app
COPY --from=build /app ./
ENTRYPOINT ["dotnet", "DockerManagement.BlazorServer.dll"]
