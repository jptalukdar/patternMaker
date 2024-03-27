import React, { useRef, useEffect } from 'react'

const Canvas = props => {
  
  const canvasRef = useRef(null)
  
  function draw(ctx, frameCount) {
    // ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height)
    ctx.fillStyle = '#000000'
    ctx.moveTo(20, 20);
    ctx.beginPath()
    ctx.lineTo(frameCount,frameCount)
    ctx.stroke()
  }
  
  useEffect(() => {
    
    const canvas = canvasRef.current
    const context = canvas.getContext('2d')
    let frameCount = 0
    let animationFrameId
    console.log("Play")
    
    //Our draw came here
    const render = () => {
      frameCount++
      console.log(frameCount)
      draw(context, frameCount)
      animationFrameId = window.requestAnimationFrame(render)
    }
    
    render()
    console.log("End")
    
    return () => {
      window.cancelAnimationFrame(animationFrameId)
    }


  }, [])
  
  return <canvas ref={canvasRef} {...props} width="500" height="500" className='bg-slate-100' />
}

export default Canvas