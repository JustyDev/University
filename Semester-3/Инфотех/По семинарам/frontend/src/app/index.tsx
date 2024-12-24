import './globals.css'
import {Router} from './router.tsx'
import {useEffect} from "react";
import {initialQuery} from "../pages/common/model.ts";

export const App = () => {

  useEffect(() => {
    initialQuery.start()
  }, []);

  return (
    <>
      <Router />
    </>
  )
}
