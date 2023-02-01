import { useLoaderData } from "react-router";

export default function ListView(props) {
  const list = useLoaderData()
  return (
    <div>
      Table is {props.table}
      <ul>{list.map(item => (
        <li key={item.id}>{item.Name}</li>
      ))}</ul>
    </div>
  );
}
