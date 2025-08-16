FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

COPY ["TelemetryService.csproj", "."]
RUN dotnet restore "./TelemetryService.csproj"

COPY . .
WORKDIR "/src/."
RUN dotnet build "TelemetryService.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "TelemetryService.csproj" -c Release -o /app/publish /p:UseAppHost=false

FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "TelemetryService.dll"]