import React, { useEffect } from 'react';

const NoiseOverlay: React.FC = () => {
  
  useEffect(() => {
    if (typeof window !== 'undefined') {
      generateNoiseTexture();
    }
  }, []);

  const generateNoiseTexture = (): void => {
    const canvas = document.getElementById('noiseCanvas') as HTMLCanvasElement;
    const ctx = canvas?.getContext('2d');

    if (ctx) {
      const width = window.innerWidth;
      const height = window.innerHeight;
      canvas.width = width;
      canvas.height = height;

      const imageData = ctx.createImageData(width, height);
      const data = imageData.data;
      const density = 0.13; // 13% density

      for (let i = 0; i < data.length; i += 4) {
        const isParticle = Math.random() < density;
        const alpha = isParticle ? Math.floor(Math.random() * 20) : 0; // Random transparency up to 10%
        data[i] = 255; // Red
        data[i + 1] = 255; // Green
        data[i + 2] = 255; // Blue
        data[i + 3] = alpha; // Random transparency for particles, fully transparent otherwise
      }

      ctx.putImageData(imageData, 0, 0);
    }
  };

  return (
    // Replace this with your HTML code
    <canvas className="fixed inset-0 w-full h-full pointer-events-none z-[1000]" id="noiseCanvas"></canvas>
  );
};

export default NoiseOverlay;