import React, { useState, useRef, useEffect } from 'react';

const CanvasComponent = (className) => {
  const canvasRef = useRef(null);
  const [radius, setRadius] = useState(50);

  const [X, setX] = useState(0.25);
  const [Y, setY] = useState(8);
  const [A, setA] = useState(3);
  const [N, setN] = useState(1);
  const [P, setP] = useState(2);
  const [color, setColor] = useState("#000000");
  
  const resolution = 1000;
  const sub_resolution = Array.from({ length: resolution }, (_, i) => i / resolution);
  var image_size = [400, 400];

  const radians = deg => (deg * Math.PI) / 180.0;

  const plot_function = (content, func, ...args) => {
    // context.clearRect(0, 0, canvas.width, canvas.height);
    // console.log("Plotting");
    // console.log(X,Y,A,N);

    for (let theta = 0; theta <= 360; theta++) {
      for (let s of sub_resolution) {
        const value = func(theta + s, ...args);
        const x = Math.floor(image_size[0] / 2 + value * 100 * Math.cos(radians(theta)));
        const y = Math.floor(image_size[1] / 2 + value * 100 * Math.sin(radians(theta)));
        content.lineTo(x, y);
      }
    }
  };

  const lotus = (theta, props) => {
    var rad = radians(theta);
    var a = Math.abs(Math.cos(A * rad));
    var b = P * (X - Math.abs(Math.cos(A * rad + Math.PI / 2)));
    var c = P + Y * Math.abs(Math.cos(2 * A * rad + Math.PI / 2));

    if (theta == 0){
      console.log("Lotus");
      console.log(X,Y,A,N,P);
      console.log(Math.PI)
      console.log(rad)
      console.log(Math.cos(2 * A * rad + Math.PI / 2), 2 * A * rad + Math.PI / 2, Math.PI / 2)
      console.log(c, P + Y * Math.abs(Math.cos(2 * A * rad + Math.PI / 2)))
      console.log(a, b, c, rad);
      console.log(c, typeof c);
    }
    
    return N + (a + b) / c;
  };

  useEffect(() => {
    console.log("Draw");
    const canvas = canvasRef.current;
    const context = canvas.getContext('2d');
    image_size = [canvas.width, canvas.height];


    // console.log(image_size);
    // Clear canvas
    context.clearRect(0, 0, canvas.width, canvas.height);

    context.fillStyle = "white";
    context.fillRect(0, 0, canvas.width, canvas.height);

    context.beginPath();
    // console.log(X,Y,A,N);
    // context.arc(centerX, centerY, radius, 0, 2 * Math.PI);
    plot_function(context, lotus)
    context.fillStyle = color;
    context.fill();
    context.closePath();


  }, [X,Y,A,N, P, color]);


  var download = function(){
    var link = document.createElement('a');
    link.download = 'pattern-maker.png';
    const canvas = canvasRef.current;
    link.href = canvas.toDataURL()
    link.click();
  }

  // const handleSliderChange = (event) => {
  //   setRadius(event.target.value);
  // };

  return (
    <div className='flex flex-col md:flex-row items-center gap-2 grow'>
      <canvas ref={canvasRef} className='w-full h-full border border-1 border-gray-800' width={image_size[0]} height={image_size[1]} />
      <div className='flex flex-col gap-2 px-8 w-full md:min-w-30 '>

      <label>Petel Separation: {X}</label>
      <input type="range" min="0" max="2" step="0.05" value={X} className='w-full' onChange={e => setX(Number(e.target.value))} />


      <label>Petel Skew: {Y}</label>
      <input type="range" min="-1" max="20" value={Y} className='w-full' onChange={e => setY(Number(e.target.value))} />
      
      <label>Petel Bloat: {P}</label>
      <input type="range" min="-1" max="20" value={P} className='w-full' onChange={e => setP(Number(e.target.value))} />
      
      <label>No of petals: {2*A}</label>
      <input type="range" min="0" max="20" value={A} className='w-full' onChange={e => setA(Number(e.target.value))} />

      <label>Zoom: {N}</label>
      <input type="range" min="0" max="2" step="0.1" value={N} className='w-full' onChange={e => setN(Number(e.target.value))} />

      <label>Fill Color: {color}</label>
      <input
        type="color"
        value={color}
        onChange={(e) => setColor(e.target.value)}
      />

      <button onClick={download} className='px-2 py-1 border-gray-800 border border-2'>
        Download
      </button>

      </div>
    </div>
  );
};

export default CanvasComponent;