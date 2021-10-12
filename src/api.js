import axios from "axios";

// const host = "localhost:10000";
const host = "http://161.35.178.247:10000";

export const uploadFile = async (file, epsg) => {
  console.log("... uploading file");
  const url = `http://${host}/api/file`;
  let formData = new FormData();
  formData.append("file", file);
  formData.append("code", epsg);
  const response = await axios.post(url, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
  console.log(response.data.message);
  console.log(response.data.points.length);
  return response.data;
};
