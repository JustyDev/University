import {Header} from "@widgets/header";
import {Outlet} from "react-router-dom";

export const MainLayout = () => {
  return (
    <div>
      <Header/>

      <Outlet/>
    </div>
  )
}