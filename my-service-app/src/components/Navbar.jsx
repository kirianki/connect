import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="bg-blue-500 text-white p-4">
      <div className="container mx-auto flex justify-between">
        <Link to="/" className="text-lg font-bold">Service Finder</Link>
        <div>
          <Link to="/dashboard" className="px-4">Dashboard</Link>
        </div>
      </div>
    </nav>
  );
}
