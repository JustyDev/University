import {BrowserRouter, Route, Routes} from 'react-router-dom';
import {CommonPage} from '@/pages/common';
import {ResultPage} from '@/pages/result';
import {MainLayout} from "@widgets/main-layout";
import {HistoryPage} from "@/pages/history";
import {MantineProvider} from "@mantine/core";

import '@mantine/core/styles.css';

export function App() {
  return (
    <MantineProvider>
      <BrowserRouter>
        <Routes>
          <Route element={<MainLayout/>}>
            <Route path="/" element={<CommonPage/>}/>
            <Route path="/result/:id" element={<ResultPage/>}/>
            <Route path="/history" element={<HistoryPage/>}/>
          </Route>
        </Routes>
      </BrowserRouter>
    </MantineProvider>
  );
}
