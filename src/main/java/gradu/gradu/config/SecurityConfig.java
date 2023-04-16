//package gradu.gradu.config;
//
//import org.springframework.context.annotation.Bean;
//import org.springframework.context.annotation.Configuration;
//import org.springframework.security.authentication.AuthenticationManager;
//import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
//import org.springframework.security.config.annotation.web.builders.HttpSecurity;
//import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
//import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
//import org.springframework.security.crypto.password.PasswordEncoder;
//import org.springframework.security.web.SecurityFilterChain;
//import org.springframework.security.web.util.matcher.AntPathRequestMatcher;
//
//@Configuration
//@EnableWebSecurity
//public class SecurityConfig {
//    @Bean
//    SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
//        //기본 설정 : 모든 사이트 접근 허용
//         http.authorizeHttpRequests().requestMatchers(
//                 new AntPathRequestMatcher("/**")).permitAll()
//                 //로그인 : 로그인 주소(매핑), 로그인 성공시 url
//                 .and()
//                 .formLogin()
//                 .loginPage("/login")
//                 .defaultSuccessUrl("/login")
//
//                 //로그아웃 : 로그아룻 주소 (매핑), 로그아웃 성공시 url , 로그아웃시 사용자세션 종료
//                 .and()
//                 .logout()
//                 .logoutRequestMatcher(new AntPathRequestMatcher("/login"))
//                 .logoutSuccessUrl("/login")
//                 .invalidateHttpSession(true);
//
//         return http.build();
//    }
//    //비밀번호 암호화
//    @Bean
//    PasswordEncoder passwordEncoder() {
//        return new BCryptPasswordEncoder();
//    }
//    //AuthenticationManager는 스프링 시큐리티의 인증을 담당
//    // 생성될 때 스프링의 내부 동작으로 인해, UserSecurity와 PasswordEncoded가 자동으로 설정된다.
//    @Bean
//    AuthenticationManager authenticationManager(AuthenticationConfiguration authenticationConfiguration) throws Exception{
//        return authenticationConfiguration.getAuthenticationManager();
//    }
//}
