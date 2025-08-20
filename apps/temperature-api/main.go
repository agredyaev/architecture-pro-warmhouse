package main

import (
	"encoding/json"
	"fmt"
	"log"
	"math/rand"
	"net/http"
	"strings"
	"time"
)

type TemperatureResponse struct {
	Value       float64   `json:"value"`
	Unit        string    `json:"unit"`
	Timestamp   time.Time `json:"timestamp"`
	Location    string    `json:"location"`
	Status      string    `json:"status"`
	SensorID    string    `json:"sensor_id"`
	SensorType  string    `json:"sensor_type"`
	Description string    `json:"description"`
}

func temperatureHandler(w http.ResponseWriter, r *http.Request) {
	sensorID := strings.TrimPrefix(r.URL.Path, "/temperature/")
	location := r.URL.Query().Get("location")

	if location == "" {
		switch sensorID {
		case "1":
			location = "Living Room"
		case "2":
			location = "Bedroom"
		case "3":
			location = "Kitchen"
		default:
			location = "Unknown"
		}
	}

	if sensorID == "" {
		switch location {
		case "Living Room":
			sensorID = "1"
		case "Bedroom":
			sensorID = "2"
		case "Kitchen":
			sensorID = "3"
		default:
			sensorID = "0"
		}
	}

	rand.Seed(time.Now().UnixNano())
	temperature := 15.0 + rand.Float64()*(30.0-15.0)

	response := TemperatureResponse{
		Value:       temperature,
		Unit:        "°C",
		Timestamp:   time.Now(),
		Location:    location,
		Status:      "active",
		SensorID:    sensorID,
		SensorType:  "temperature",
		Description: "Temperature reading",
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func main() {
	http.HandleFunc("/temperature/", temperatureHandler)
	fmt.Println("Temperature API is running on port 8081")
	log.Fatal(http.ListenAndServe(":8081", nil))
}