package main

import (
	"encoding/json"
	"fmt"
	"log"
	"math/rand"
	"net/http"
	"time"
)

type TemperatureResponse struct {
	SensorID    string  `json:"sensorId"`
	Location    string  `json:"location"`
	Temperature float64 `json:"temperature"`
}

func temperatureHandler(w http.ResponseWriter, r *http.Request) {
	location := r.URL.Query().Get("location")
	sensorID := r.URL.Query().Get("sensorId")

	// Logic from README.md to determine location/sensorId if one is missing
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
	// Generate a random temperature between 15.0 and 30.0
	temperature := 15.0 + rand.Float64()*(30.0-15.0)

	response := TemperatureResponse{
		SensorID:    sensorID,
		Location:    location,
		Temperature: temperature,
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func main() {
	http.HandleFunc("/temperature", temperatureHandler)
	fmt.Println("Temperature API is running on port 8081")
	log.Fatal(http.ListenAndServe(":8081", nil))
}