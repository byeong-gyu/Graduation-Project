package gradu.gradu.controller;

import gradu.gradu.dto.MemberDTO;
import gradu.gradu.service.MemberService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import javax.servlet.http.HttpSession;
import javax.validation.Valid;

@Controller
@RequiredArgsConstructor
public class MemberController {

    private final MemberService memberService;

    @GetMapping("/")
    public String indexForm() {
        return "main";
    }


    @GetMapping("/join")
    public String joinForm(){
        return "join";
    }

    @PostMapping("/auth/join")
    public String join(MemberDTO memberDTO, Model model){

        memberService.save(memberDTO);
        model.addAttribute("message", "회원가입을 성공하셨습니다");
        model.addAttribute("searchUrl","/");

        return "message";

    }
    @ExceptionHandler(IllegalArgumentException.class)
    public String handlerException(IllegalArgumentException ex, Model model) {
        model.addAttribute("message", ex.getMessage());
        model.addAttribute("searchUrl", "/join");
        return "message";
    }

    @GetMapping("/login")
    public String loginForm(){
     return "login";
    }

    @PostMapping("auth/login")
    public String login(@ModelAttribute MemberDTO memberDTO, HttpSession session, Model model){
        MemberDTO loginResult= memberService.login(memberDTO);
        if(loginResult!=null) {
            session.setAttribute("userID", loginResult.getUserID());
            model.addAttribute("message","로그인 성공");
            model.addAttribute("searchUrl","/");
            return "message";
        } else {
            model.addAttribute("message","아이디 혹은 비밀번호가 틀립니다");
            model.addAttribute("searchUrl","/login");
         return "message";
        }
    }

    @GetMapping("/logoutAction")
    public String logout(HttpSession session,Model model) {
        session.getAttribute(session.getId());
        session.invalidate();
        return "redirect:/";
    }



}
