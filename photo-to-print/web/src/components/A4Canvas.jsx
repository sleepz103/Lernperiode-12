import React, { useRef } from "react";
import { Stage, Layer, Image as KonvaImage } from "react-konva";
import useImage from "use-image";

// A4 dimensions in pixels at 300 DPI
const A4_WIDTH = 3508;
const A4_HEIGHT = 2480;

// Simple tile layout algorithm
function layoutPositions(count) {
  const cols = Math.ceil(Math.sqrt(count));
  const rows = Math.ceil(count / cols);
  const cellW = A4_WIDTH / cols;
  const cellH = A4_HEIGHT / rows;
  const positions = [];

  for (let i = 0; i < count; i++) {
    const col = i % cols;
    const row = Math.floor(i / cols);
    positions.push({
      x: col * cellW,
      y: row * cellH,
      width: cellW,
      height: cellH,
    });
  }
  return positions;
}

export default function A4Canvas({ images }) {
  const stageRef = useRef(null);
  const positions = layoutPositions(images.length);

  const exportToPng = () => {
    const uri = stageRef.current.toDataURL({ pixelRatio: 1 });
    const link = document.createElement("a");
    link.download = "a4-layout.png";
    link.href = uri;
    link.click();
  };

  return (
    <div className="bg-white rounded-xl shadow p-4">
      <Stage width={A4_WIDTH / 4} height={A4_HEIGHT / 4} ref={stageRef} scale={{ x: 0.25, y: 0.25 }}>
        <Layer>
          {images.map((img, i) => (
            <Tile key={img.name} src={img.src} {...positions[i]} />
          ))}
        </Layer>
      </Stage>

      <div className="flex justify-center mt-4">
        <button
          onClick={exportToPng}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Export PNG
        </button>
      </div>
    </div>
  );
}

function Tile({ src, x, y, width, height }) {
  const [image] = useImage(src);
  return <KonvaImage image={image} x={x} y={y} width={width} height={height} />;
}
