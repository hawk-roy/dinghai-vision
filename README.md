# Dinghai Vision

**English** | [中文](README.zh-CN.md)

Dinghai Vision is an experimental AI aquarium vision monitoring project.

The goal of this project is to build a first-version MVP for a home aquarium monitoring system using a camera, Raspberry Pi, computer vision models, fish trajectory tracking, behavior feature extraction, and abnormal activity alerts.

The project is currently in the early prototype stage.

## Project Background

Many aquarium owners want to remotely check whether their fish are active and whether abnormal behavior has occurred while they are away.

This project explores a pure-vision approach:

- Capture aquarium video with a camera.
- Run fish detection on Raspberry Pi.
- Track fish movement over time.
- Calculate behavior features.
- Detect abnormal activity using simple rules.
- Generate local status and event data.
- Later upload data to a cloud server and display it on a mobile client.

The first version does not include water temperature, pH, TDS, water level, leakage detection, or other physical sensors.

## Project Codename

Dinghai Vision is inspired by the Chinese classic *Journey to the West*.

"Dinghai" refers to the idea of guarding and stabilizing water, inspired by the story of the Dragon Palace and the Ruyi Jingu Bang, also known as the Dinghai Shenzhen. "Vision" represents the AI camera system used to monitor the aquarium.

## MVP Goal

The first MVP focuses on a minimal technical loop:

```text
Camera
  ↓
Raspberry Pi
  ↓
Fish Detection Model
  ↓
Bounding Boxes
  ↓
Fish Center Points
  ↓
Trajectory Tracking
  ↓
Behavior Feature Calculation
  ↓
Abnormal Event Rules
  ↓
Local JSON / CSV Output
  ↓
Cloud Upload / Mobile Display
```

The first target scene is a small test tank or transparent box with one fish, fixed camera position, stable lighting, and a clean background.

## First Version Scope

The first version aims to support:

- Camera video capture
- Local image and video saving
- Fish detection using YOLO / Fishial / custom-trained model
- Bounding box output
- Fish center point calculation
- Single-fish trajectory recording
- Basic behavior feature calculation
- Abnormal event generation
- Local `status.json`, `events.json`, and `tracks.csv` output
- Future cloud upload and mobile display

## Not Included in the First Version

The first version will not attempt to support:

- Fish disease diagnosis
- Confirmed oxygen deficiency detection
- Real water quality measurement
- Algae outbreak prediction
- Multi-fish long-term identity recognition
- Complex multi-object tracking
- 24/7 cloud video streaming
- Automatic control of pumps, lights, feeders, or heaters
- Commercial hardware enclosure design

## Planned Hardware

Prototype hardware may include:

- Raspberry Pi 4 Model B
- Intel RealSense D405 camera or other USB/RGB camera
- Small test tank or transparent box
- Local development machine
- Optional lightweight cloud server for later testing

## Software Stack

Planned technologies:

- Python for camera capture, OpenCV processing, model inference, and behavior analysis
- OpenCV for video processing
- YOLO / Fishial / custom fish detection model for fish detection
- CSV / JSON for local output
- Golang for future cloud server API
- SQLite or PostgreSQL for future data storage
- Web dashboard or WeChat Mini Program for future display

## Core Concept

The fish detection model does not directly determine whether a fish is sick or healthy.

The model only answers a simpler question:

```text
Where is the fish in this frame?
```

The project then uses multiple frames over time to calculate movement and behavior.

The general logic is:

```text
Detection result
  ↓
Fish bounding box
  ↓
Fish center point
  ↓
Trajectory over time
  ↓
Behavior features
  ↓
Rule-based abnormal event
```

## Core Data

### Detection Output

The fish detection model is expected to return data similar to:

```json
[
  {
    "class": "fish",
    "confidence": 0.91,
    "bbox": [120, 180, 260, 240]
  }
]
```

The bounding box format is:

```text
[x1, y1, x2, y2]
```

The fish center point can be calculated as:

```text
center_x = (x1 + x2) / 2
center_y = (y1 + y2) / 2
```

### Status Output

Example `status.json`:

```json
{
  "device_id": "tank_001",
  "timestamp": "2026-07-24T15:20:30+08:00",
  "fish_count": 1,
  "activity_score": 0.76,
  "avg_speed": 18.4,
  "top_ratio": 0.12,
  "middle_ratio": 0.71,
  "bottom_ratio": 0.17,
  "status": "normal"
}
```

### Event Output

Example `events.json`:

```json
[
  {
    "device_id": "tank_001",
    "timestamp": "2026-07-24T15:22:10+08:00",
    "event_type": "low_activity",
    "level": "warning",
    "message": "Low fish activity detected. Please check the aquarium.",
    "features": {
      "duration_sec": 600,
      "avg_speed": 2.1,
      "bottom_ratio": 0.82,
      "total_distance": 130
    }
  }
]
```

### Trajectory Output

Example `tracks.csv`:

```csv
timestamp,track_id,center_x,center_y,speed,region
15:20:01,1,320,180,12.5,middle
15:20:02,1,335,185,15.8,middle
15:20:03,1,340,260,21.3,bottom
```

## Behavior Features

The first version may calculate the following behavior features:

- `fish_count`
- `avg_speed`
- `max_speed`
- `total_distance`
- `activity_score`
- `top_ratio`
- `middle_ratio`
- `bottom_ratio`
- `stationary_time_sec`
- `turning_score`
- `circling_score`

These features are calculated from the fish center point trajectory over time.

## Abnormal Event Rules

The first version may include simple rule-based events:

- `low_activity`
- `bottom_stay`
- `surface_stay`
- `possible_circling`

These events are not medical diagnoses. They are only visual behavior alerts intended to help the user check the aquarium earlier.

Example rule:

```text
If a fish stays in the bottom region for a long time
and its average speed is lower than the normal threshold,
generate a bottom_stay warning.
```

Another example:

```text
If the fish moves a long total distance
but remains near the same local area
and changes direction frequently,
generate a possible_circling warning.
```

## Development Roadmap

### Milestone 1: Camera Capture

Goals:

- Connect camera to Raspberry Pi or development machine.
- Capture raw video.
- Save images and short video clips locally.

Expected output:

```text
raw_video.mp4
sample_frame.jpg
```

### Milestone 2: Fish Detection

Goals:

- Run a detection model on aquarium video.
- Draw bounding boxes around detected fish.
- Save an annotated output video.

Expected output:

```text
annotated_video.mp4
```

### Milestone 3: Trajectory Tracking

Goals:

- Calculate fish center points.
- Record center point movement over time.
- Save trajectory data to CSV.

Expected output:

```text
tracks.csv
```

### Milestone 4: Behavior Analysis

Goals:

- Calculate speed, distance, activity score, and region ratio.
- Generate local status data.

Expected output:

```text
status.json
```

### Milestone 5: Abnormal Event Detection

Goals:

- Add simple abnormal behavior rules.
- Generate local abnormal event data.
- Save related screenshots or short clips.

Expected output:

```text
events.json
event_snapshot.jpg
event_clip.mp4
```

### Milestone 6: Cloud Upload

Goals:

- Upload status and event data to a cloud server.
- Provide basic API endpoints for latest status and event history.

Possible API endpoints:

```text
POST /api/device/heartbeat
POST /api/device/status
POST /api/device/event
POST /api/device/snapshot
GET  /api/device/latest
GET  /api/device/events
```

### Milestone 7: Mobile Display

Goals:

- Display latest status, snapshots, and event records on a web page or mini program.
- Show fish activity state and abnormal event history.

## Current Development Principle

The project follows a local-first MVP strategy:

```text
Run locally first.
Validate detection.
Validate trajectory.
Validate behavior features.
Validate abnormal events.
Then connect cloud.
Then build mobile UI.
```

Do not start with a full mobile application or real-time cloud video streaming before the local vision loop is stable.

## Recommended Development Order

The recommended development order is:

1. Camera capture
2. Local video saving
3. Fish detection
4. Bounding box visualization
5. Center point calculation
6. Trajectory recording
7. Behavior feature calculation
8. Abnormal event rules
9. Local JSON / CSV output
10. Cloud upload
11. Web or mini program display
12. Real-time video, if needed later

## Repository Structure

Planned structure:

```text
dinghai-vision/
├── README.md
├── README.zh-CN.md
├── docs/
│   ├── product_mvp.md
│   ├── data_format.md
│   └── roadmap.md
├── experiments/
│   ├── camera_capture/
│   ├── detection_test/
│   └── behavior_analysis/
├── edge/
│   ├── camera/
│   ├── detection/
│   ├── tracking/
│   ├── behavior/
│   └── output/
├── cloud/
│   └── api/
├── mobile/
│   └── mini_program/
├── data/
│   ├── samples/
│   └── labels/
└── scripts/
```

This structure may change as the project evolves.

## Development Notes

### Local Prototype First

The first prototype should run locally without cloud dependency.

A successful local prototype should be able to:

- Capture video from the camera.
- Detect fish in the video.
- Draw bounding boxes.
- Record fish center points.
- Generate trajectory data.
- Calculate basic behavior features.
- Generate local status and event files.

### Cloud Later

Cloud upload should be added only after the local vision pipeline is stable.

The cloud server should initially handle:

- Device heartbeat
- Status upload
- Event upload
- Snapshot upload
- Latest status query
- Event history query

### Mobile UI Last

The mobile interface should be added after the cloud API has stable real data.

The first mobile interface can be very simple:

- Device online/offline status
- Latest snapshot
- Current fish count
- Activity score
- Latest abnormal event
- Event history list

## License Notice

This project may experiment with third-party models and libraries such as YOLO, Fishial, OpenCV, and other open-source tools.

Before any commercial use, all third-party licenses must be reviewed carefully, especially:

- Model source code
- Model weights
- Training datasets
- Inference libraries
- Deployment tools
- Cloud SDKs

## Disclaimer

This project is an experimental prototype.

It does not provide veterinary diagnosis, water quality measurement, or guaranteed fish health assessment.

Any abnormal behavior alert should be treated as a reminder for the user to manually check the aquarium.

## Status

Current stage:

```text
Early prototype planning
```

Next target:

```text
Camera capture and local fish detection test
```