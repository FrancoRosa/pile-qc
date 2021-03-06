import { DeckGL } from "@deck.gl/react";
import { NavigationControl, StaticMap } from "react-map-gl";
import { ColumnLayer, ScatterplotLayer } from "@deck.gl/layers";
import { useRef, useState } from "react";
import FileInput from "./FileInput";
import { useStoreState } from "easy-peasy";
import mapboxgl from "mapbox-gl";

// eslint-disable-next-line import/no-webpack-loader-syntax
mapboxgl.workerClass =
  // eslint-disable-next-line import/no-webpack-loader-syntax
  require("worker-loader!mapbox-gl/dist/mapbox-gl-csp-worker").default;

const MAPBOX_ACCESS_TOKEN =
  "pk.eyJ1Ijoia20xMTVmcmFuY28iLCJhIjoiY2t0eXQ3cHBhMGI3aTMxcG14dnN0OHJveSJ9.LWxkBiVPF9UfGWMI4sWakQ";

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
  const [showSearch, setShowSearch] = useState(false);
  const [found, setFound] = useState([]);
  const [targetPile, setTargetPile] = useState({});
  const [relatedPoints, setRelatedPoints] = useState([]);
  const searchInput = useRef(null);

  const points = useStoreState((state) => state.points);
  const file = useStoreState((state) => state.file);

  const INITIAL_VIEW_STATE = {
    longitude: points.length > 3 ? points[3].lng_field : -93,
    latitude: points.length > 3 ? points[3].lat_field : 40,
    zoom: 21,
    maxZoom: 25,
    pitch: 60,
    bearing: 0,
  };
  const [view, setView] = useState(INITIAL_VIEW_STATE);

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

  const handleCloseSearch = () => {
    setShowSearch(false);
  };

  const handleShowSearch = () => {
    setShowSearch(true);
    setShowUpload(false);
  };

  const handleShowUpload = () => {
    setShowUpload(true);
    setShowSearch(false);
  };

  const handleSearch = () => {
    const query = searchInput.current.value.toLowerCase();
    console.log(query);
    const result = points.filter((point) =>
      point.pile_id.toLowerCase().includes(query)
    );
    result.splice(10);
    setFound(result);
  };

  const handlePileSearch = (f) => {
    setView({
      ...view,
      latitude: f.lat_design,
      longitude: f.lng_design,
    });
    setTargetPile(f);
  };

  return (
    <>
      <DeckGL
        initialViewState={view}
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
        {showSearch && (
          <ScatterplotLayer
            lineWidthMaxPixels={3}
            lineWidthMinPixels={2}
            getRadius={3}
            data={[targetPile]}
            getPosition={(d) => [d.lng_design, d.lat_design]}
            getColor={[100, 10, 10, 30]}
            getFillColor={[100, 10, 10, 30]}
            getLineColor={[100, 10, 10, 30]}
            filled={true}
            stroked={true}
            opacity={0.5}
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
          <hr />
          {file && <p>Current file: {file}</p>}
          <hr />
          <button className="button" onClick={handleCloseUpload}>
            Close
          </button>
        </div>
      )}
      {!showUpload && (
        <div className="upload animate__animated animate__fadeInLeft">
          <button onClick={handleShowUpload}>Upload</button>
        </div>
      )}
      {showSearch && (
        <div className="search animate__animated animate__fadeInLeft">
          <h1>Search pile</h1>
          <input type="text" ref={searchInput} />
          <button onClick={handleSearch}>Search</button>
          <hr />
          {found.map((f) => (
            <p className="pile-list" onClick={() => handlePileSearch(f)}>
              {f.pile_id}
            </p>
          ))}
          <hr />

          <button className="button" onClick={handleCloseSearch}>
            Close
          </button>
        </div>
      )}
      {!showSearch && !showUpload && (
        <div className="search animate__animated animate__fadeInLeft">
          <button onClick={handleShowSearch}>Search</button>
        </div>
      )}
    </>
  );
};

export default App;
