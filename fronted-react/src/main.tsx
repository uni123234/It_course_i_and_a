import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { router } from './router'
import App from './App'
import "./styles/tailwind.css";
import './index.css'


createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App router={router} />
  </StrictMode>,
)
