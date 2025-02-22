import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import { Link } from "react-router-dom";

export default function ProviderDashboard() {
  const { user, logout } = useContext(AuthContext);

  if (!user) return <p>Loading...</p>;

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold">Welcome, {user.full_name}</h1>
      <p>Email: {user.email}</p>
      <Link to={`/provider/${user.id}`} className="text-blue-500">View Profile</Link>
      <Link to="/edit-profile" className="block bg-blue-500 text-white p-2 rounded mt-4 text-center">Edit Profile</Link>
      <Link to="/upload-portfolio" className="block bg-green-500 text-white p-2 rounded mt-4 text-center">Upload Portfolio Images</Link>
      <button onClick={logout} className="bg-red-500 text-white p-2 rounded mt-4">Logout</button>
    </div>
  );
}
