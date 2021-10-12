import { DeckGL } from "@deck.gl/react";
import { NavigationControl, StaticMap } from "react-map-gl";
import { ColumnLayer, ScatterplotLayer } from "@deck.gl/layers";
import points from "./result.json";
import { useState } from "react";
import FileInput from "./FileInput";

const MAPBOX_ACCESS_TOKEN =
  "pk.eyJ1Ijoia20xMTVmcmFuY28iLCJhIjoiY2t0eXQ3cHBhMGI3aTMxcG14dnN0OHJveSJ9.LWxkBiVPF9UfGWMI4sWakQ";

const INITIAL_VIEW_STATE = {
  longitude: points[3].lng_field,
  latitude: points[3].lat_field,
  zoom: 21,
  maxZoom: 25,
  pitch: 60,
  bearing: 0,
};

const colors = {
  black: [0, 0, 0],
  blue: [0, 0, 255],
  brown: [165, 42, 42],
  darkblue: [0, 0, 139],
  green: [0, 255, 0],
  lightblue: [135, 206, 235],
  lightgreen: [144, 238, 144],
  orange: [255, 165, 0],
  pink: [255, 105, 180],
  purple: [128, 0, 128],
  red: [255, 0, 0],
  white: [255, 255, 255],
  yellow: [255, 255, 0],
};

const colorsFill = {
  black: [0, 0, 0, 128],
  blue: [0, 0, 255, 128],
  brown: [165, 42, 42, 128],
  darkblue: [0, 0, 139, 128],
  green: [0, 255, 0, 128],
  lightblue: [135, 206, 235, 128],
  lightgreen: [144, 238, 144, 128],
  orange: [255, 165, 0, 128],
  pink: [255, 105, 180, 128],
  purple: [128, 0, 128, 128],
  red: [255, 0, 0, 128],
  white: [255, 255, 255, 128],
  yellow: [255, 255, 0, 128],
};

const get_color = (point) => {
  if ("angle_g_error" in point) {
    const { angle_g_error, x_g_error, y_g_error } = point;
    const angle_th = 0.69;
    const x_th = 0.25;
    const y_th = 0.5;
    if (angle_g_error > angle_th) {
      return colorsFill.pink;
    }
    if (x_g_error > x_th) {
      return colorsFill.orange;
    }
    if (y_g_error[0] > y_th || y_g_error[1] > y_th) {
      return colorsFill.red;
    }
    return colorsFill.lightgreen;
  } else {
    return colorsFill.lightblue;
  }
};

const App = () => {
  const [showInfo, setShowInfo] = useState(false);
  const [showUpload, setShowUpload] = useState(false);
  const [relatedPoints, setRelatedPoints] = useState([]);

  const handlePileClick = (d) => {
    const { order } = d.object;

    const upperEdge = points.filter(
      (p) => p.order[0] === order[0] && p.order[1] === order[1] - 1
    )[0];
    const lowerEdge = points.filter(
      (p) => p.order[0] === order[0] && p.order[1] === order[1] + 1
    )[0];

    setRelatedPoints([upperEdge, d.object, lowerEdge]);
    setShowInfo(true);
  };

  const handleCloseButton = () => {
    document.querySelector(".details").classList.add("animate__fadeOutRight");
    setTimeout(() => {
      setShowInfo(false);
      setRelatedPoints([]);
    }, 1000);
  };

  const handleCloseUpload = () => {
    setShowUpload(false);
  };

  return (
    <>
      <DeckGL
        initialViewState={INITIAL_VIEW_STATE}
        controller={true}
        getTooltip={({ object }) =>
          object &&
          `Order: [${object.order}]
          Code: ${object.pile_id}\n\
          angle: ${object.angle_g_error}\n\
          Xdiff: ${object.x_g_error}\n\
          Ydiff: ${object.y_g_error}`
        }
      >
        <StaticMap mapboxApiAccessToken={MAPBOX_ACCESS_TOKEN}>
          <NavigationControl />
        </StaticMap>
        <ColumnLayer
          data={points}
          diskResolution={6}
          radius={0.2}
          extruded={true}
          pickable={true}
          elevationScale={1}
          getPosition={(d) => [d.lng_field, d.lat_field]}
          getFillColor={(d) => get_color(d)}
          getLineColor={[0, 0, 0]}
          getElevation={(d) => 2 + d.z_field - d.z_design}
          onClick={handlePileClick}
        />

        <ColumnLayer
          data={points}
          diskResolution={6}
          radius={0.2}
          extruded={true}
          elevationScale={1}
          getPosition={(d) => [d.lng_design, d.lat_design]}
          getFillColor={[0, 30, 0, 30]}
          getLineColor={[10, 10, 10, 30]}
          getElevation={2}
          wireframe
        />
        {showInfo && (
          <ScatterplotLayer
            lineWidthMaxPixels={3}
            lineWidthMinPixels={2}
            getRadius={3}
            data={relatedPoints}
            getPosition={(d) => [d.lng_design, d.lat_design]}
            getColor={[10, 10, 10, 30]}
            getFillColor={[10, 10, 10, 30]}
            getLineColor={[10, 10, 10, 30]}
            filled={true}
            stroked={true}
            opacity={0.8}
          />
        )}
      </DeckGL>
      {showInfo && (
        <div className="details card animate__animated animate__fadeInRight">
          <h1>Target pile:</h1>
          <p>Pile id: {relatedPoints[1].pile_id}</p>
          <p>N design: {relatedPoints[1].y_design}</p>
          <p>E design: {relatedPoints[1].x_design}</p>
          <p>Lat design: {relatedPoints[1].lat_design}</p>
          <p>Lng design: {relatedPoints[1].lng_design}</p>
          <hr />
          <p
            className={relatedPoints[1].angle_g_error < 0.69 ? "green" : "red"}
          >
            Angle error: {relatedPoints[1].angle_g_error}
          </p>
          <p className={relatedPoints[1].x_g_error < 0.25 ? "green" : "red"}>
            Easting error: {relatedPoints[1].x_g_error}
          </p>
          <p
            className={
              relatedPoints[1].y_g_error[0] < 0.25 ||
              relatedPoints[1].y_g_error[1] < 0.25
                ? "green"
                : "red"
            }
          >
            Northing error: {relatedPoints[1].y_g_error[0]},{" "}
            {relatedPoints[1].y_g_error[0]}
          </p>
          <button className="button" onClick={handleCloseButton}>
            Close
          </button>
        </div>
      )}
      {showUpload && (
        <div className="upload animate__animated animate__fadeInLeft">
          <h1>Upload file</h1>
          <FileInput />
          <button className="button" onClick={handleCloseUpload}>
            Close
          </button>
        </div>
      )}
      {!showUpload && (
        <div className="upload animate__animated animate__fadeInLeft">
          <button onClick={() => setShowUpload(true)}>Upload</button>
        </div>
      )}
    </>
  );
};

export default App;
