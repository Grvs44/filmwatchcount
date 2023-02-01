import {
  Link, Outlet,
} from 'react-router-dom';

export default function Home(props) {
  return (
    <div>
      <p>Welcome to Film Watch Count</p>
      <ul>
        <li><Link to={'filmgroup'}>Film groups</Link></li>
        <li><Link to={'film'}>Films</Link></li>
        <li><Link to={'filmwatch'}>Film watches</Link></li>
      </ul>
      <Outlet/>
    </div>
  );
}