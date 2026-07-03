import { useState } from "react";
import axios from "axios";

const Upload = () => {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleFileChange = (e) => {
    setFiles(Array.from(e.target.files));
  };

  const handleSubmit = async () => {
    if (files.length === 0) {
      alert("Please select one or more files.");
      return;
    }

    const formData = new FormData();

    files.forEach((file) => {
      formData.append("files", file);
    });

    try {
      setLoading(true);

      const response = await axios.post(
        "http://127.0.0.1:8000/documents/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      console.log(response.data);
      setResult(response.data);

      alert("Documents uploaded successfully!");
    } catch (error) {
      console.error(error);

      if (error.response) {
        alert(error.response.data.detail || "Upload failed");
      } else {
        alert("Cannot connect to backend.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-container">
      <h2>Upload Documents</h2>

      <input
        type="file"
        multiple
        onChange={handleFileChange}
      />

      <br />
      <br />

      {files.length > 0 && (
        <>
          <h3>Selected Files</h3>

          <ul>
            {files.map((file, index) => (
              <li key={index}>{file.name}</li>
            ))}
          </ul>
        </>
      )}

      <button onClick={handleSubmit} disabled={loading}>
        {loading ? "Uploading..." : "Submit"}
      </button>

      {result && (
        <div style={{ marginTop: "30px" }}>
          <h3>Backend Response</h3>

          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default Upload;