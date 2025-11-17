import React, { useState, useRef } from 'react'

export default function MockInterview(){
  const [recording, setRecording] = useState(false)
  const mediaRef = useRef<MediaRecorder | null>(null)

  // This is a minimal placeholder; full implementation requires permissions and server streaming
  return (
    <main className="p-8">
      <h2 className="text-2xl">Mock Interview (demo)</h2>
      <p>Record audio or upload an answer. Streaming and AI evaluation are performed on the server.</p>
      <button onClick={() => setRecording(r => !r)} className="mt-4 p-2 bg-blue-600 text-white">{recording? 'Stop' : 'Start'} Recording</button>
    </main>
  )
}
