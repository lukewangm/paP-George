import NavLink from "./components/NavLink";

export default function Home() {
  return (
    <div className="mt-10 mx-auto text-center">
    <div className="mt-36 text-center prose mx-auto">
      <h1 className="lg:text-5xl text-3xl font-bold">
        Determine your illness by reading similiar doctors reports
      </h1>
      <h3 className="lg:text-xl text-lg text-gray-500 font-normal mt-2 mb-3 ">
        5% of diseases are left undiagnosed. Let's diagnose them!
      </h3>
        <NavLink
          href="/start"
          className="block font-medium text-sm text-white bg-gray-800 hover:bg-gray-600 active:bg-gray-900 md:inline"
        >
          Try it
        </NavLink>
    </div>
  </div>
  );
}
