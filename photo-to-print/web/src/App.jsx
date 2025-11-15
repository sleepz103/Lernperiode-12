import React, { useState } from "react";
import A4Canvas from "./components/A4Canvas";

export default function App() {
  const [images, setImages] = useState([]);

  const handleFiles = (e) => {
    const files = Array.from(e.target.files);
    const urls = files.map((file) => ({
      name: file.name,
      src: URL.createObjectURL(file),
    }));
    setImages(urls);
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-6">
      <h1 className="text-2xl font-bold mb-4">A4 Photo Layout Generator</h1>
      <input
        type="file"
        multiple
        accept="image/*"
        onChange={handleFiles}
        className="mb-4"
      />
      {images.length > 0 && <A4Canvas images={images} />}
    </div>
  );
}
