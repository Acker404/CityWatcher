import { useState,useEffect} from 'react'
import reactLogo from './assets/react.svg'
import ReactPlayer from 'react-player'
import viteLogo from '/vite.svg'
import axios from 'axios'

import './App.css'

function App() {
  //狀態管理
  const [backendStatus, setBackendStatus] = useState("檢查中");

  const [inputUrl, setIputUrl] = useState('https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8');

  const [playingurl, setPlayingurl] = useState('https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8');

  useEffect(() => {
    axios.get('http://localhost:8000/')
    .then(response => {
      setBackendStatus(`🟢 連線成功: ${response.data.message}`)
    })
    .catch(error => {
      setBackendStatus('🔴 連線失敗 (請確認backend/main.py 有執行)')
      console.error(error)
    })
  }, []);

  const handelPlay = () => {
    if(inputUrl){
      setPlayingurl(inputUrl);
    }
  }
  
  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <div className="max-w-4xl mx-auto">
        <header className="mb-8 border-b border-gray-700 pb-4">
          <h1 className="text-3xl font-bold text-blue-400">CityWatcher 智慧交通監控</h1>
          <p classname="tetx-sm text-gray-400 mt-2">後端狀態: {backendStatus}</p>
        </header>
      </div>
    </div> 
  )
}

export default App
