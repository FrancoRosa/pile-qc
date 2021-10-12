import { useEffect, useState } from "react";
import { uploadFile } from "./api";

const FileInput = () => {
  const [path, setPath] = useState("");
  const [name, setName] = useState("Nothing selected yet");
  const [fileStatus, setFileStatus] = useState({});

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
    uploadFile(file)
      .then((res) => {
        setFileStatus(res);
      })
      .catch(() => setFileStatus({ message: false }));
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
        {fileStatus.message ? (
          <div className="is-flex is-align-content-center is-flex-direction-column">
            <p
              className={
                fileStatus.message ? "has-text-success" : "has-text-fail"
              }
            >
              {fileStatus.message ? "Success" : "Fail"}
            </p>
            <p>Piles found: {fileStatus.points.length}</p>
          </div>
        ) : (
          ""
        )}
      </div>
    </div>
  );
};

export default FileInput;
