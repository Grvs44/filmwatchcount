import {
  createBrowserRouter,
} from 'react-router-dom';

import Home from './pages/Home';
import ListView from './pages/ListView';
import { loadData } from './loaders';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <Home />,
    errorElement: <div>That page couldn't be found</div>,
  },
  {
    path: '/filmgroup',
    element: <ListView table={'filmgroup'} />,
    loader: (page=1) => loadData('filmgroup', page),
  },
])