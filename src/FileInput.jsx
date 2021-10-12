import { useStoreActions, useStoreState } from "easy-peasy";
import { useEffect, useState } from "react";
import { uploadFile } from "./api";

const FileInput = () => {
  const [path, setPath] = useState("");
  const [name, setName] = useState("Nothing selected yet");
  const [fileStatus, setFileStatus] = useState(null);
  const [loading, setLoading] = useState(false);

  const setPoints = useStoreActions((actions) => actions.setPoints);
  const points = useStoreState((state) => state.points);
  const setFile = useStoreActions((actions) => actions.setFile);

  useEffect(() => {
    const handleFiles = (e) => {
      let localPath = e.target.files[0];
      let localName = e.target.files[0].name;
      setPath(localPath);
      setName(localName);
    };

    const inputElement = document.querySelector(".file-input");
    inputElement.addEventListener("change", handleFiles, false);
  }, []);

  const handleFiles = (file) => {
    setFileStatus(null);
    setLoading(true);
    uploadFile(file)
      .then((res) => {
        setFileStatus(res.message);
        setPoints(res.points);
        setLoading(false);
        setFile(name);
      })
      .catch(() => {
        setFileStatus(false);
        setPoints([]);
        setLoading(false);
      });
  };

  return (
    <div className="columns">
      <div className="column file has-name">
        <label className="file-label">
          <input className="file-input" type="file" accept=".csv, .xlsx" />
        </label>
      </div>
      <div className="column">
        {path ? (
          <div className="is-flex is-justify-content-center">
            <button
              className="button is-outlined is-success"
              onClick={() => handleFiles(path)}
            >
              Upload
            </button>
          </div>
        ) : (
          ""
        )}
      </div>
      <div className="column">
        {loading && (
          <p className="animate__animated animate__zoomIn animate__infinite">
            ... Processing{" "}
          </p>
        )}
        {fileStatus ? (
          <div className="is-flex is-align-content-center is-flex-direction-column">
            <p className={fileStatus ? "has-text-success" : "has-text-fail"}>
              {fileStatus ? "Success" : "Fail"}
            </p>
            <p>Piles found: {points.length}</p>
          </div>
        ) : (
          ""
        )}
      </div>
      <br />
    </div>
  );
};

export default FileInput;
