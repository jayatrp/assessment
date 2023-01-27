$population_data = @{}



$response = Invoke-RestMethod -Uri "https://datausa.io/api/data?drilldowns=State&measures=Population"

$jsonData = $response.data | ConvertFrom-Json

foreach($item in $response.data) {
    $data = $item.data
    $state = $item.State
    $year = $item.Year
    $population = $item.Population
    if (-not $population_data.ContainsKey($state)) {
        $population_data[$state] = @{}
    }
    $population_data[$state][$year] = $population
}

$csvfile = "population_generate.csv"
$csvContent = 
"State Name, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2019 Factors`n"
foreach($state in $population_data.Keys) {
    $population_change_list = @()
    foreach($year in $population_data[$state].Keys) {
        if($year -eq "2019 Factors") {
            $factors = (prime_factors $population_data[$state][$year]) -join ';'
            $population_data[$state][$year] = "$($population_data[$state][$year]) ($factors)"
        } elseif ($year -ne "2013") {
            $prev_population = $population_data["$state"][$(int($year) - 1)]
            $population_change_list += population_change $prev_population $population_data[$state][$year]
            $population_data[$state][$year] = "$($population_data[$state][$year]) $($population_change_list[-1])"
        }
    }
    $csvContent += "$state, $($population_data[$state].Values -join ', ')`n"
}

Set-Content -Path $csvfile -Value $csvContent