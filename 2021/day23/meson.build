project('day23', 'cpp', default_options : ['cpp_std=c++20',])

abseil = dependency('abseil', fallback: ['abseil-cpp', 'absl_container_dep'])

executable('day23',
           sources: ['day23.cpp'],
           dependencies: [abseil])

executable('day23-2',
           sources: ['day23-2.cpp'],
           dependencies: [abseil])
