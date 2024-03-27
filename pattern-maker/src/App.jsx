import { useState, useRef } from 'react'
import Canvas from './Canvas';
import CanvasComponent from './PlotCanvas';
function App() {


  return (
    <>
        <div className='container h-screen'>
          <div className='flex  flex-col h-full items-center justify-center bg-gray-200 rounded-lg p-8 min-h-32 min-w-32'>
          <h1 className='text-6xl font-bold py-2 pb-8 text-center'>Flower Maker</h1>
          <CanvasComponent className='grow' />
          </div>
        </div>
    </>
  );
}

export default App
