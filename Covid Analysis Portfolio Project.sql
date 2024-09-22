Select *
From PortfolioProject..CovidDeaths
Where continent is not null
order by 3,4

--Select *
--From PortfolioProject..CovidVaccinations
--order by 3,4

--Select Data that will be used

Select Location, Date, Total_cases, New_cases, Total_Deaths, Population
From PortfolioProject..CovidDeaths
Where continent is not null
order by 1,2

-- Looking at Total Cases vs Total Deaths
-- Likeklihood of dying if contracted Covid in the United States

Select Location, Date, Total_Cases, Total_Deaths, (total_deaths/total_cases)*100 as DeathPercentage
From PortfolioProject..CovidDeaths
Where Location like '%states%'
and continent is not null
order by 1,2

--Looking at Total Cases vs Population
--Shows Percentage of Population contracted Covid

Select Location, Date, Population, Total_cases, (total_cases/Population)*100 as ContractedPercentage
From PortfolioProject..CovidDeaths
Where Location like '%states%'
and continent is not null
order by 1,2

--Looking at Countries with highest Contraction Rate compared to Population

Select Location, Population, Max(total_cases) as HighestContractionCount, Max((total_cases/Population))*100 as ContractedPercentage
From PortfolioProject..CovidDeaths
Group by Location, Population
order by ContractedPercentage desc

--Shows Countries with Highest Death Count per Population

Select Location, Max(cast(total_deaths as int)) as TotalDeathCount
From PortfolioProject..CovidDeaths
--Where Location like '%states%'
Where continent is not null
Group by Location, Population
order by TotalDeathCount desc

--Break Down by Continent

Select Continent, Max(cast(total_deaths as int)) as TotalDeathCount
From PortfolioProject..CovidDeaths
--Where Location like '%states%'
Where continent is not null
Group by continent
order by TotalDeathCount desc

--Showing Continent with Highest Death Count

Select Continent, Max(cast(total_deaths as int)) as TotalDeathCount
From PortfolioProject..CovidDeaths
--Where Location like '%states%'
Where continent is not null
Group by continent
order by TotalDeathCount desc

--Global

Select Sum(new_cases) as Total_Cases, Sum(cast(new_deaths as int)) as Total_Deaths, Sum(cast(new_deaths as int))/Sum(new_cases)*100 as DeathPercentage
From PortfolioProject..CovidDeaths
--Where Location like '%states%'
Where continent is not null
--Group by Date
order by 1,2


--Looking at Total Population vs Vaccinations

Select dea.Continent, dea.Location, dea.Date, dea.Population, vac.new_vaccinations
, Sum(Convert(int, vac.new_vaccinations)) Over (Partition by dea.Location Order by dea.Location, dea.Date) as RollingPeopleVaccinated
--, (RollingPeopleVaccinated/population) * 100
From PortfolioProject..CovidDeaths dea
Join PortfolioProject..CovidVaccinations vac
	On dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null
order by 1,2,3

--Use CTE

With PopvsVac (Continent, Location, Date, Population, New_Vaccinations, RollingPeopleVaccinated)
as
(
Select dea.Continent, dea.Location, dea.Date, dea.Population, vac.new_vaccinations
, Sum(Cast(vac.new_vaccinations as int)) Over (Partition by dea.Location Order by dea.Location, dea.Date) as RollingPeopleVaccinated
--, (RollingPeopleVaccinated/population)*100
From PortfolioProject..CovidDeaths dea
Join PortfolioProject..CovidVaccinations vac
	On dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null
--order by 1,2,3
)

Select *, (RollingPeopleVaccinated/Population)*100
From PopvsVac


--Temp Table

Create Table #PercentPopulationVaccinated
(
Continent nvarchar(255),
Location nvarchar(255),
Date datetime,
Population numeric,
New_vaccinations numeric,
RollingPeopleVaccinated numeric,
)


Insert into #PercentPopulationVaccinated
Select dea.Continent, dea.Location, dea.Date, dea.Population, vac.new_vaccinations
, Sum(Cast(vac.new_vaccinations as int)) Over (Partition by dea.Location Order by dea.Location, dea.Date) as RollingPeopleVaccinated
--, (RollingPeopleVaccinated/population)*100
From PortfolioProject..CovidDeaths dea
Join PortfolioProject..CovidVaccinations vac
	On dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null
--order by 1,2,3

Select *, (RollingPeopleVaccinated/Population)*100
From #PercentPopulationVaccinated


--Create View to Store For Visualization

Create View PercentPopulationVaccinated as 
Select dea.Continent, dea.Location, dea.Date, dea.Population, vac.new_vaccinations
, Sum(Cast(vac.new_vaccinations as int)) Over (Partition by dea.Location Order by dea.Location, dea.Date) as RollingPeopleVaccinated
--, (RollingPeopleVaccinated/population)*100
From PortfolioProject..CovidDeaths dea
Join PortfolioProject..CovidVaccinations vac
	On dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null
--order by 1,2,3

Select *
From PercentPopulationVaccinated