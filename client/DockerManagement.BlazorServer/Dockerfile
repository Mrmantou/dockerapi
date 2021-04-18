#See https://aka.ms/containerfastmode to understand how Visual Studio uses this Dockerfile to build your images for faster debugging.

FROM mcr.microsoft.com/dotnet/aspnet:5.0 AS base
WORKDIR /app
EXPOSE 80

FROM mcr.microsoft.com/dotnet/sdk:5.0 AS build
WORKDIR /src
COPY ["client/DockerManagement.BlazorServer/DockerManagement.BlazorServer.csproj", "client/DockerManagement.BlazorServer/"]
RUN dotnet restore "client/DockerManagement.BlazorServer/DockerManagement.BlazorServer.csproj"
COPY . .
WORKDIR "/src/client/DockerManagement.BlazorServer"
RUN dotnet build "DockerManagement.BlazorServer.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "DockerManagement.BlazorServer.csproj" -c Release -o /app/publish

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "DockerManagement.BlazorServer.dll"]
